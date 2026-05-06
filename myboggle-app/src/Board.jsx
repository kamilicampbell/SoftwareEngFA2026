import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import React from 'react';
import './Board.css';

function Board({ board }) {

  function tile(id, letter) {
    return (
      <Grid key={id} item>
        <div className="Tile">
          <Paper elevation={4}>
            {letter}
          </Paper>
        </div>
      </Grid>
    );
  }

  function rowOfTiles(id, rowObj) {
    return (
      <Grid
        key={id}
        container
        spacing={2}
        justifyContent="center"
        wrap="nowrap"
      >
        {Object.keys(rowObj).map((letterKey) =>
          tile(letterKey + id, rowObj[letterKey])
        )}
      </Grid>
    );
  }

  function gridOfRows(board) {
    return (
      <>
        {Object.keys(board).map((rowKey) =>
          rowOfTiles(rowKey, board[rowKey])
        )}
      </>
    );
  }

  return (
    <div className="Board-div">
      <div className="Board-container">
        <Grid container direction="column" spacing={2}>
          {gridOfRows(board)}
        </Grid>
      </div>
    </div>
  );
}

export default Board;
