 
# evaluate.py
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall
from chains.vector_chain import get_vector_qa_chain

def run_evaluation():
    print("Starting evaluation...")
    
    questions = [
        "What is the main purpose of the createStore function?",
        "How do you subscribe to state changes in Redux?",
        "What does a reducer function do?",
    ]
    ground_truths = [
        "The createStore function creates a Redux store that holds the complete state tree of your app.",
        "You can subscribe to state changes using the store.subscribe(listener) method.",
        "A reducer is a pure function that takes the previous state and an action, and returns the next state.",
    ]

    qa_chain = get_vector_qa_chain()
    answers = []
    contexts = []
    for question in questions:
        result = qa_chain.invoke({"query": question})
        answers.append(result["result"])
        contexts.append([doc.page_content for doc in result["source_documents"]])

    ds = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })

    result = evaluate(ds, metrics=[faithfulness, answer_relevancy, context_recall])
    print("Evaluation complete.")
    df = result.to_pandas()
    print(df)

if __name__ == "__main__":
    run_evaluation()