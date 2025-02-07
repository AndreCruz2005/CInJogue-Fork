import { useState } from "react";
import "./styles/styles.scss";

function App() {
  interface AIOuput {
    command: string;
    titles: string[];
    other: string[];
  }

  // State to store the output from GENAI
  const [output, setOutput] = useState<string>("");

  // State for the input value
  const [prompt, setPrompt] = useState<string>("");

  async function GENAI(prompt: string): Promise<AIOuput> {
    const response = await fetch(`http://127.0.0.1:3000/genai/${prompt}`);
    if (!response.ok) {
      throw new Error(`Falha em comunicar com o backend: ${response.status}`);
    }

    const data: AIOuput = await response.json();
    return data;
  }

  async function handleSubmit() {
    try {
      // Call GENAI with the prompt and set the result in the output
      const result = await GENAI(prompt);
      setOutput(JSON.stringify(result)); // Set the output in a string format
    } catch (error) {
      console.error(error);
      setOutput("Failed to fetch data.");
    }
  }

  return (
    <div className="App">
      <label id="Label">PROMPT:</label>
      <input
        id="Prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)} // Update state as input changes
      />
      <button id="Submit" onClick={handleSubmit}>
        SUBMIT
      </button>
      <textarea id="OutputBox" value={output} disabled={true} />
    </div>
  );
}

export default App;
