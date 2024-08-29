import spacy
from spacy.matcher import Matcher
from tkinter import Tk, filedialog

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the Matcher with the shared vocabulary
matcher = Matcher(nlp.vocab)

# Define patterns for different categories
customer_requirements_patterns = [
    [{"LOWER": "budget"}, {"IS_PUNCT": True, "OP": "?"}, {"IS_DIGIT": True}],
    [{"LOWER": "safety"}, {"LOWER": "concern"}],
    [{"LOWER": "preference"}],
    [{"LOWER": "transmission"}, {"IS_PUNCT": True, "OP": "?"}, {"IS_ALPHA": True}],
    [{"LOWER": "vehicle"}, {"LOWER": "size"}],
]

policy_patterns = [
    [{"LOWER": "inspection"}],
    [{"LOWER": "warranty"}],
    [{"LOWER": "categories"}],
    [{"LOWER": "buy-back"}],
    [{"LOWER": "test"}, {"LOWER": "drive"}],
]

objection_patterns = [
    [{"LOWER": "resale"}, {"LOWER": "value"}],
    [{"LOWER": "vehicle"}, {"LOWER": "condition"}],
]

# Add patterns to the matcher
matcher.add("CUSTOMER_REQUIREMENTS", customer_requirements_patterns)
matcher.add("POLICY_INSPECTION", policy_patterns)
matcher.add("CUSTOMER_OBJECTIONS", objection_patterns)


# Function to load a file and extract content
def load_file():
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select a Text File", filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        return text
    else:
        print("No file selected.")
        return None


# Function to process the text and extract attributes with values
def process_text(text):
    doc = nlp(text)

    # Apply the matcher to the doc
    matches = matcher(doc)

    # Debugging: Check if any matches are found
    if not matches:
        print("No matches found. Check the patterns or input text.")

    # Create a dictionary to store extracted information
    extracted_info = {
        "CUSTOMER_REQUIREMENTS": [],
        "POLICY_INSPECTION": [],
        "CUSTOMER_OBJECTIONS": []
    }

    # Extract and categorize matched phrases
    for match_id, start, end in matches:
        match_label = nlp.vocab.strings[match_id]
        span = doc[start:end]
        value = span.sent  # Captures the entire sentence as context
        if match_label in extracted_info:
            extracted_info[match_label].append(value.text.strip())

    # Print extracted information
    for category, items in extracted_info.items():
        if items:
            print(f"{category}:")
            for item in items:
                print(f"  - {item}")


# Main function to load file and process text
def main():
    text = load_file()

    if text:
        process_text(text)


# Run the main function
if __name__ == "__main__":
    main()





