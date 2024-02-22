import './App.css';
import CastawayList from './components/CastawayList';
import castaways from './data/season_46_castaways.json';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Fantasy Survivor Ranking Assistant</h1>
      </header>
      <CastawayList castawayList={castaways} />
    </div>
  );
}

export default App;
