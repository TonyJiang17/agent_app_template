from database import Database
from schema.models_new import Roadmap, Topic, SubTopic, Quiz, QuizQuestion, QuizChoice, Resource
from datetime import datetime

def test_roadmap():
    print("\n=== Testing Roadmap Operations ===")
    db = Database()
    
    # Create a roadmap
    roadmap = Roadmap(
        slug="python-beginner-roadmap",
        title="Python Beginner's Roadmap",
        description="A comprehensive guide to Python programming for beginners",
        topics=[
            Topic(
                slug="python-fundamentals",
                name="Python Fundamentals",
                subtopics=[
                    SubTopic(
                        slug="variables-and-types",
                        name="Variables and Data Types",
                        completed=False
                    ),
                    SubTopic(
                        slug="control-flow",
                        name="Control Flow",
                        completed=True
                    )
                ]
            ),
            Topic(
                slug="python-oop",
                name="Object-Oriented Programming",
                subtopics=[
                    SubTopic(
                        slug="classes-and-objects",
                        name="Classes and Objects",
                        completed=False
                    ),
                    SubTopic(
                        slug="inheritance",
                        name="Inheritance",
                        completed=False
                    )
                ]
            )
        ]
    )
    
    # Save roadmap
    roadmap_id = db.create_roadmap(roadmap)
    print(f"Created roadmap with ID: {roadmap_id}")
    
    # Retrieve roadmap
    saved_roadmap = db.get_roadmap(roadmap_id)
    if saved_roadmap:
        print(f"Retrieved roadmap: {saved_roadmap.model_dump_json(indent=2)}")
    else:
        print("Failed to retrieve roadmap")
    
    return roadmap_id



def main():
    try:
        print("Starting database tests...")
        # Test all operations
        roadmap_id = test_roadmap()
        
        print("\nAll tests completed successfully!")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")

if __name__ == "__main__":
    main()
