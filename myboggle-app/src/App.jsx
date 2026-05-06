import React, { useState, useEffect } from 'react';
import { GAME_STATE } from './GameState.js';
import Board from './Board.jsx';
import GuessInput from './GuessInput.jsx';
import FoundSolutions from './FoundSolutions.jsx';
import SummaryResults from './SummaryResults.jsx';
import ToggleGameState from './ToggleGameState.jsx';
import './App.css';

function App() {
  const [allSolutions, setAllSolutions] = useState([]);
  const [foundSolutions, setFoundSolutions] = useState([]);
  const [gameState, setGameState] = useState(GAME_STATE.BEFORE);
  const [grid, setGrid] = useState([]);
  const [totalTime, setTotalTime] = useState(0);
  const [size, setSize] = useState(3);
  const [game, setGame] = useState({});

  useEffect(() => {
    if (typeof game.solution_words !== "undefined") {
      setAllSolutions(game.solution_words);
    }
  }, [game]);

  useEffect(() => {
    if (gameState === GAME_STATE.IN_PROGRESS && Object.keys(game).length === 0) {
      fetch(`/api/game/${size}/`)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          console.log("API data:", data);
          window._currentGameId = data.id;
          setGame(data);
          if (data.grid) {
            setGrid(data.grid);
          }
          setFoundSolutions([]);
        })
        .catch((err) => {
          console.log("Fetch error:", err.message);
        });
    }
  }, [gameState]);

  useEffect(() => {
    if (gameState === GAME_STATE.BEFORE) {
      setGame({});
      setGrid([]);
      setAllSolutions([]);
      setFoundSolutions([]);
    }
  }, [gameState]);

  function correctAnswerFound(answer) {
    setFoundSolutions(prev => [...prev, answer]);
    setAllSolutions(prev => prev.filter(w => w !== answer));
  }

  return (
    <div className="App">
      <h1 className="App-title">🔤 Boggle</h1>
      <ToggleGameState
        gameState={gameState}
        setGameState={(state) => setGameState(state)}
        setSize={(state) => setSize(state)}
        setTotalTime={(state) => setTotalTime(state)}
        numFound={foundSolutions.length}
        setGrid={(g) => { setGrid(g); }}
      />
      {gameState === GAME_STATE.IN_PROGRESS &&
        <div>
          <Board board={grid} />
          <GuessInput
            allSolutions={allSolutions}
            foundSolutions={foundSolutions}
            correctAnswerCallback={(answer) => correctAnswerFound(answer)}
          />
          <FoundSolutions headerText="Solutions you've found" words={foundSolutions} />
        </div>
      }
      {(gameState === GAME_STATE.ENDED || gameState === GAME_STATE.ADD_LEADERBOARD) &&
        <div>
          <Board board={grid} />
          <SummaryResults words={foundSolutions} totalTime={totalTime} />
          <FoundSolutions headerText="Missed Words" words={allSolutions} />
        </div>
      }
    </div>
  );
}

export default App;
