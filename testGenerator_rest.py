from flask_restful import reqparse
from flasgger import Swagger, swag_from
from flask import Flask,jsonify
from flask_cors import CORS
import os
import uuid 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from TestGenerator.testGenerator import TestGenerator
from TestGenerator.assistant import Assistant
import settings

app = Flask(__name__)
CORS(app, supports_credentials=True)  
conf_path = os.path.abspath(__file__)
conf_path = os.path.dirname(conf_path) 
conf_path = os.path.join(conf_path, 'TestGenerator/swagger.yaml')
swagger = Swagger(app=app, template_file=conf_path)

MIN_NUM_TEST_CASES = 1
MAX_NUM_TEST_CASES = 1000
TAVILY_KEY = settings.TAVILY_KEY
API_KEY = settings.API_KEY

# Define Database Schema using SQLAlchemy ORM
Base = declarative_base() 

class TestGeneratorDB(Base):
    __tablename__ = 'test_generators'

    id = Column(String, primary_key=True)
    assistant_id = Column(String)    
    num_test_cases = Column(Integer)
    category = Column(String)
    style = Column(String)
    technique = Column(String)
    

#  Flask routes definitions here    
@app.route('/check', methods=['GET']) 
@swag_from('TestGenerator/swagger.yaml')
def check():
    return{'message': 'TestGenerator API created successfully'}
                
@app.route('/createTestGenerator', methods=['POST']) 
@swag_from('TestGenerator/swagger.yaml') 
def createTestGenerator():
    # Parse request parameters
    parser = reqparse.RequestParser()
    parser.add_argument('assistant_id', type=str, required=True, help="Assistant ID is required")
    parser.add_argument('num_test_cases', type=int, required=False, default=5, help="Number of test cases") 
    parser.add_argument('category', type=str, required=False, default="random", help="Category")
    parser.add_argument('style', type=str, required=False, default="random", help="Prompting style")
    parser.add_argument('technique', type=str, required=False, default="random", help="Persuasion technique")
    args = parser.parse_args()

    test_generator_id = str(uuid.uuid4())
    
    # Save TestGenerator to the database 
    test_generator_db = TestGeneratorDB(id=test_generator_id, assistant_id=args['assistant_id'],num_test_cases=args['num_test_cases'], category=args['category'], style=args['style'], technique=args['technique'])
    session.add(test_generator_db)
    session.commit()
    session.close()

    return {'message': 'TestGenerator instance created successfully', 'test_generator_id': test_generator_id}

@app.route('/generateTestcases/<test_generator_id>', methods=['PUT']) 
@swag_from('TestGenerator/swagger.yaml')
def generateTestcasesByTestGenerator(test_generator_id):
   if test_generator_id:    
       test_generator_db = session.query(TestGeneratorDB).filter_by(id=test_generator_id).first() 
       session.close()
       if test_generator_db:
          assistant = Assistant(API_KEY) 
          parser = reqparse.RequestParser()
          parser.add_argument('web_browsing', type=bool, required=True, default=False, help="Web broswing enabled")
          args = parser.parse_args()  
          web_browsing=args['web_browsing']       
          if web_browsing:
              assistant.updateWebBrowsing(web_browsing, TAVILY_KEY)
          assistant.retrieveAssistant(test_generator_db.assistant_id)   
          instance = TestGenerator(assistant, test_generator_db.num_test_cases, test_generator_db.category, test_generator_db.style, test_generator_db.technique)
          testcase = instance.generateTestcases()
          
          return testcase  
   else:
       return {'message': 'An internal error ocurred when generating test cases'}
   

@app.route('/generateTestcases', methods=['POST']) 
@swag_from('TestGenerator/swagger.yaml')
def generateTestcases():

      parser = reqparse.RequestParser()
      parser.add_argument('assistant_id', type=str, required=True, help="Assistant ID is required")
      parser.add_argument('num_test_cases', type=int, required=False, default=5, help="Number of test cases") 
      parser.add_argument('category', type=str, required=False, default="random", help="Category")
      parser.add_argument('style', type=str, required=False, default="random", help="Prompting style")
      parser.add_argument('technique', type=str, required=False, default="random", help="Persuasion technique")
      parser.add_argument('web_browsing', type=bool, required=False, default=False, help="Web browsing enabled")
      args = parser.parse_args()
      

      assistant = Assistant(API_KEY) 
   
      web_browsing=args['web_browsing']       
      if web_browsing:
          assistant.updateWebBrowsing(web_browsing, TAVILY_KEY)
      assistant.retrieveAssistant(args['assistant_id']) 
      instance = TestGenerator(assistant, args['num_test_cases'], args['category'], args['style'], args['technique'])
      testcase = instance.generateTestcases()
      
      if testcase:        
          return testcase  
      else:
          return {'message': 'An internal error ocurred when generating test cases'}

   
@app.route('/testGenerator', methods=['GET'])       
@swag_from('TestGenerator/swagger.yaml')
def getTestgenerators():
    test_generator_db = session.query(TestGeneratorDB).all()
    session.close()
    if test_generator_db:       
        result = []
        for test_generator in test_generator_db:
            result.append({
                'id': test_generator.id,
                'assistant_id': test_generator.assistant_id,
                'num_test_cases': test_generator.num_test_cases,
                'category': test_generator.category,
                'style': test_generator.style,
                'technique': test_generator.technique
            })
        return jsonify(result)     
    else: 
        return {'message': 'An internal error ocurred when generating test cases'}
     
@app.route('/updateTestGenerator/<test_generator_id>', methods=['PUT'])  
@swag_from('TestGenerator/swagger.yaml')
def updateTestgenerator(test_generator_id):
   if test_generator_id:   
       test_generator_db = session.query(TestGeneratorDB).filter_by(id=test_generator_id).first() 
       
       if test_generator_db:
           # Parse request parameters
           parser = reqparse.RequestParser()
           parser.add_argument('assistant_id', type=str, required=False, default=test_generator_db.assistant_id, help="Assistant ID")
           parser.add_argument('num_test_cases', type=int, required=False, default=test_generator_db.num_test_cases, help="Number of test cases")
           parser.add_argument('category', type=str, required=False, default=test_generator_db.category, help="Category")
           parser.add_argument('style', type=str, required=False, default=test_generator_db.category, help="Prompting style")
           parser.add_argument('technique', type=str, required=False, default=test_generator_db.category, help="Persuasion technique")
           args = parser.parse_args()
        
           num_test_cases=args['num_test_cases']
           category=args['category'] 
           assistant_id=args['assistant_id'] 
           style=args['style'] 
           technique=args['technique'] 
           
           if assistant_id:          
               test_generator_db.assistant_id = assistant_id
               
           if num_test_cases and isinstance(num_test_cases, int):         
               test_generator_db.num_test_cases = num_test_cases
                   
           if category and isinstance(category, str):
               test_generator_db.category = category   
               
           if style and isinstance(style, str):
               test_generator_db.style = style 
               
           if technique and isinstance(technique, str):
               test_generator_db.technique = technique 
               
               
           session.commit()
          
           return jsonify({'message': 'TestGenerator updated successfully'}), 200 
       
       else:
            return jsonify({'error': 'TestGenerator not found'}), 404
        
       session.close()  
             
@app.route('/deleteTestGenerator/<test_generator_id>', methods=['DELETE'])
@swag_from('TestGenerator/swagger.yaml')
def deleteTestGenerator(test_generator_id):
    if test_generator_id:   
 
        test_generator_db = session.query(TestGeneratorDB).filter_by(id=test_generator_id).first()
        
        if test_generator_db: 
            session.delete(test_generator_db)
            session.commit() 
            return jsonify({'message': 'TestGenerator deleted successfully'}), 200 
        else:
            return jsonify({'error': 'TestGenerator not found'}), 404
        session.close()

@app.route('/testGenerator/<test_generator_id>', methods=['GET'])       
@swag_from('TestGenerator/swagger.yaml')
def getTestgenerator(test_generator_id):
    if test_generator_id:   
        test_generator_db = session.query(TestGeneratorDB).filter_by(id=test_generator_id).first() 
        session.close()
        if test_generator_db:       
           return jsonify({'id':test_generator_db.id, 'assistant_id': test_generator_db.assistant_id, 'num_test_cases': test_generator_db.num_test_cases, 'category': test_generator_db.category, 'style': test_generator_db.style, 'technique': test_generator_db.technique})    
    else:
        return {'message': 'An internal error ocurred when generating test cases'}
    
@app.route('/deleteAllTestGenerators', methods=['DELETE'])
@swag_from('TestGenerator/swagger.yaml') 
def deleteAllTestGenerators():
    test_generator_db = session.query(TestGeneratorDB).delete()
    if test_generator_db:
        session.commit()
        return jsonify({'message': 'All test generators deleted successfully'}), 200 
    else:
        return jsonify({'error': 'Test generator not found'}), 404

    session.close()
               

if __name__ == "__main__":
   
    # Establish Database Connection
    engine = create_engine('sqlite:///test_generators.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Run the Flask app
    app.run(debug=False, host="0.0.0.0", port=5000)
