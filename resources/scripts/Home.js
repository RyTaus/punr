class Home extends React.Component {
    render() {
        return (
          <div>
          {this.props.children}
              <div id="homeblurb">
                <h1 class="titles"> Welcome to Compundium! </h1>
                <h2 class="titles"> A site for lovers of the pun. Share and like other puns to your heart's puntent. </h2>
              </div>
              <img class="center-block" id = "homephoto" src="/resources/images/no_pun_intended.png"/>
          </div>

      
        );
    }
}

ReactDOM.render(
    <Home />,
    document.getElementById('root')
    );