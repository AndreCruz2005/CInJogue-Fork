import { useState } from 'react'
import axios from 'axios'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  return (
    <div>
      <label>
        Username:
        <input type="text" />
      </label>
      <br />
      <label>
        Password:
        <input type="password" />
      </label>
      <br />
      <label>
        Email:
        <input type="email" />
      </label>
      <br />
      <label>
        Birthdate:
        <input type="date" />
      </label>
      <button onClick={() => SignUp()}>Submit</button>
    </div>
  );
}

function SignUp(username :string, password :string, email:string, birthdate:string) : void{
  
}

export default App
