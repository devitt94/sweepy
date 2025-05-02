
function Menu({ setDisplayMenu, setDisplayCreateForm, setDisplaySearchForm }) {

    const handleCreateButtonClick = () => () => {
        setDisplayMenu(false);
        setDisplaySearchForm(false);
        setDisplayCreateForm(true);
    };

    const handleFindButtonClick = () => () => {
        setDisplayMenu(false);
        setDisplayCreateForm(false);
        setDisplaySearchForm(true);
    };
    
  return (
    <div className="menu">
      <div className="menu__item"><button type="button" onClick={handleCreateButtonClick()}>Create Sweepstake</button></div>
      <div className="menu__item"><button type="button" onClick={handleFindButtonClick()}>Find Sweepstakes</button></div>
    </div>
  );
}

export default Menu;