import React, { useState } from 'react';
import Button from "@mui/material/Button";
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import Select from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import TextField from '@mui/material/TextField';
import { GAME_STATE } from './GameState.js';
import './ToggleGameState.css';

function ToggleGameState({ gameState, setGameState, setSize, setTotalTime, numFound, setGrid }) {
  const [buttonText, setButtonText] = useState("Start a new game!");
  const [startTime, setStartTime] = useState(0);
  const [boardSize, setBoardSize] = useState(3);
  const [leaderBoard, setLeaderBoard] = useState([]);
  const [input, setInput] = useState("");
  const [deltaTime, setDeltaTime] = useState(0);
  const [selectedGameId, setSelectedGameId] = useState(null);

  function updateGameState(endTime) {
    if (gameState === GAME_STATE.BEFORE || gameState === GAME_STATE.ENDED) {
      setStartTime(Date.now());
      setGameState(GAME_STATE.IN_PROGRESS);
      setButtonText("End game");
    } else if (gameState === GAME_STATE.IN_PROGRESS) {
      const dt = (endTime - startTime) / 1000.0;
      setDeltaTime(dt);
      setTotalTime(dt);
      setGameState(GAME_STATE.ADD_LEADERBOARD);
      setButtonText("Start a new game!");
    }
  }

  function showLeaderBoard() {
    fetch('/api/games/')
      .then(res => res.json())
      .then(data => {
        const entries = data.map(game => ({
          gameId: game.id,
          boardSize: game.size,
          numFound: game.leaderboard?.entries?.length > 0
            ? Math.max(...game.leaderboard.entries.map(e => e.words_found_count))
            : 0,
          playerName: game.leaderboard?.entries?.length > 0
            ? game.leaderboard.entries[0].user?.username || 'N/A'
            : 'No entries yet',
          theBoard: JSON.stringify(game.grid)
        }));
        setLeaderBoard(entries);
        setGameState(GAME_STATE.SHOW_LEADERBOARD);
      })
      .catch(err => console.log("Error fetching games:", err));
  }

  function handleSizeMenuChange(event) {
    setBoardSize(event.target.value);
    setSize(event.target.value);
  }

  function handleGridChange(event) {
    const selected = leaderBoard.find(
      item => item.theBoard === event.target.value
    );
    if (selected) {
      setSelectedGameId(selected.gameId);
      setGrid(JSON.parse(event.target.value));
    }
  }

  function keyPress(e) {
    if (e.key === 'Enter') {
      saveToLeaderBoard();
    }
  }

  function saveToLeaderBoard() {
    const token = localStorage.getItem('authToken');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Token ${token}`;

    const gameId = window._currentGameId;
    if (!gameId) {
      setGameState(GAME_STATE.BEFORE);
      return;
    }

    const body = { words_found_count: numFound, total_time_seconds: Math.round(deltaTime) };
    if (!token) body.user_id = 1;

    fetch(`/api/games/${gameId}/leaderboard/`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    })
      .then(res => res.json())
      .then(() => setGameState(GAME_STATE.BEFORE))
      .catch(err => {
        console.log("Error saving leaderboard:", err);
        setGameState(GAME_STATE.BEFORE);
      });
  }

  return (
    <div>
      {(gameState === GAME_STATE.BEFORE || gameState === GAME_STATE.ENDED) &&
        <div className="Toggle-game-state2">
          <Button variant="outlined" onClick={() => showLeaderBoard()}>
            Load Challenge
          </Button>
        </div>
      }
      <div className="Toggle-game-state">
        {gameState === GAME_STATE.ADD_LEADERBOARD &&
          <TextField
            id="outlined-basic"
            label="Enter Your Name"
            variant="outlined"
            onKeyDown={(e) => keyPress(e)}
            onChange={(event) => setInput(event.target.value)}
          />
        }
        {gameState !== GAME_STATE.ADD_LEADERBOARD &&
          gameState !== GAME_STATE.SHOW_LEADERBOARD &&
          <Button variant="outlined" onClick={() => updateGameState(Date.now())}>
            {buttonText}
          </Button>
        }
        {gameState === GAME_STATE.SHOW_LEADERBOARD &&
          <Button variant="outlined" onClick={() => {
            if (selectedGameId) {
              setGameState(GAME_STATE.IN_PROGRESS);
              setButtonText("End game");
            } else {
              setGameState(GAME_STATE.BEFORE);
            }
          }}>
            Play Selected Game
          </Button>
        }
        {(gameState === GAME_STATE.BEFORE || gameState === GAME_STATE.ENDED) &&
          <div className="Input-select-size">
            <FormControl size="small" sx={{ minWidth: 140 }}>
              <Select
                labelId="sizelabel"
                id="sizemenu"
                value={boardSize}
                onChange={handleSizeMenuChange}
              >
                <MenuItem value={3}>3</MenuItem>
                <MenuItem value={4}>4</MenuItem>
                <MenuItem value={5}>5</MenuItem>
                <MenuItem value={6}>6</MenuItem>
                <MenuItem value={7}>7</MenuItem>
                <MenuItem value={8}>8</MenuItem>
                <MenuItem value={9}>9</MenuItem>
                <MenuItem value={10}>10</MenuItem>
              </Select>
              <FormHelperText>Set Grid Size</FormHelperText>
            </FormControl>
          </div>
        }
        {gameState === GAME_STATE.SHOW_LEADERBOARD &&
          <div className="Input-select-size">
            <FormControl size="small" sx={{ minWidth: 250 }}>
              <Select
                labelId="leaderboardlabel"
                id="leaderboardmenu"
                value=''
                onChange={handleGridChange}
              >
                {leaderBoard.map((item, idx) => (
                  <MenuItem key={idx} value={item.theBoard}>
                    Size: {item.boardSize} | High Score: {item.numFound} | {item.playerName}
                  </MenuItem>
                ))}
              </Select>
              <FormHelperText>Select Game</FormHelperText>
            </FormControl>
          </div>
        }
      </div>
    </div>
  );
}

export default ToggleGameState;
