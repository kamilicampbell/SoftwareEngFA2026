import React, { useState } from 'react';
import TextField from "@mui/material/TextField";
import './GuessInput.css';

function GuessInput({ allSolutions, foundSolutions, correctAnswerCallback }) {
  const [labelText, setLabelText] = useState("Make your first guess!");
  const [input, setInput] = useState("");

  function evaluateInput() {
    const upperInput = input.toUpperCase();
    if (foundSolutions.includes(upperInput)) {
      setLabelText(upperInput + " has already been found!");
    } else if (allSolutions.includes(upperInput)) {
      correctAnswerCallback(upperInput);
      setLabelText(upperInput + " is correct!");
    } else {
      setLabelText(upperInput + " is incorrect!");
    }
    setInput("");
  }

  function keyPress(e) {
    if (e.key === 'Enter') {
      evaluateInput();
    }
  }

  return (
    <div className="Guess-input">
      <div>{labelText}</div>
      <TextField
        value={input}
        onKeyDown={(e) => keyPress(e)}
        onChange={(event) => setInput(event.target.value)}
        label="Enter Guess"
        variant="outlined"
        size="small"
      />
    </div>
  );
}

export default GuessInput;
