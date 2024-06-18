import { Button } from '../common/Button';

function Header() {
  
    return (
      <>
        <Button text="Quote" onClick={() => { window.location.href = "/quote"; }}></Button>
        <Button text="Partners" onClick={() => { window.location.href = "/partners"; }}></Button>

      </>
    )
  }
  
  export default Header