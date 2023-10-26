import openai
import json
import os
# Set your OpenAI API key
openai.api_key = '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'

record_file_path = '/Users/devaduttsanka/Desktop/Masters/Fall-2023/NLP/Final_Project/data2.json'

def is_unique(content):
    if not os.path.exists(record_file_path):
        return True
    with open(record_file_path, 'r') as f:
        existing_content = f.read()
    return content not in existing_content


def save_to_json_file(new_data):
    file_path = record_file_path
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
        combined_data = existing_data + new_data
    else:
        combined_data = new_data
    
    with open(file_path, 'w') as f:
        json.dump(combined_data, f, indent=4)

def generate_story_and_questions(event_type):
    # Define the prompt for story generation
    story_prompt = f"""

                    Generate a 5-sentence long story following the given event type and conditions. 

                    Event type: {event_type}

                    Conditions 1: The story involves many events and actions related to {event_type}. 
                    Condition 2: These events and actions will have spatial and temporal changes. 
                    Condition 3: The temporal and spatial changes needed to be coherent, so it is possible to ask reasoning questions based on these changes. 

                    """
    story_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=story_prompt,
        max_tokens=1850
    )
    story_text = story_response['choices'][0]['text'].strip()


    # Define the prompt for question generation
    # questions_prompt = f"Based on the following story, generate 5 questions with 4 possible answer choices and provide the correct answer with a reason.\n\nStory:\n{story_text}"
    
    questions_prompt = f"""
                    Use the story {story_text} and generate 5 questions with 4 possible answer choices realted to the story. 
                    
                    The conditions mentioned below need to be followed while generating questions and answer choices.  

                    Condition 1: The questions needed to be composed of both temporal and spatial information from the context. Anything explicitly mentioned is the context should be discarded for question generation. 
                    Condition 2: The question need to be asked in some way, so reasoning is needed to find the correct answer. 

                    Generate the answers and the reason for the answer after the question. Give correct answer and reasoning sepearetly at the end of the question and answer choices.


            """
    
    # Generate questions and answers
    questions_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=questions_prompt,
        max_tokens=1500
    )
    questions_text = questions_response['choices'][0]['text'].strip().split('\n')
    questions_text = [i.strip() for i in questions_text if i.strip()!='']
    # # Organize and store data in JSON format
    data = []
    combined_content = story_text + '\n' + '\n'.join(questions_text)
    if is_unique(combined_content):  
        try:
            for i in range(0,len(questions_text),7):
                question = questions_text[i]
                options = [questions_text[j] for j in range(i+1,i+5)]
                answer = questions_text[i+5].split(":")[1].strip()
                reason = questions_text[i+6].split(":")[1].strip()
                data.append({
                    "Story":story_text,
                    "Question": question,
                    "Answer Choices": options,
                    "Answer": answer,
                    "Reasoning": reason
                    
                })
        except Exception as e:
            print(e)
    return data

# Run the function
generate_story_and_questions("Natural and Environmental Events")
event_types = [
    "Health and Medical Events",
    "Educational and Academic Events",
    "Arts and Entertainment Events",
    "Sports and Recreation Events",
    "Environmental Conservation Events",
    "Technology and Innovation Events",
    "Cultural and Heritage Events",
    "Social and Community Events",
    "Climate and Weather Events",
    "Travel and Tourism Events",
    "Food and Culinary Events",
    "Agricultural and Farming Events",
    "Literary and Publishing Events",
    "Energy and Resources Events",
    "Transportation and Logistics Events",
    "Construction and Architecture Events",
    "Fashion and Design Events",
    "Legal and Justice Events",
    "Business and Entrepreneurship Events",
    "Humanitarian and Relief Events"
]
for event in event_types:
    generate_data = 0
    while generate_data < 50:
        data = generate_story_and_questions(event)
        if data:
            generate_data += 1
            save_to_json_file(data)

with open(record_file_path, 'r') as f:
    existing_content = f.read()

print(existing_content)