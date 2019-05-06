class Browse extends React.Component {
    render() {
        return (
          <div>
            <span className="container">
              <form action="/browse" method="post">
                <input type="hidden" name="kind" value="search"></input>
                <input id="search" type="text" name="q" placeholder='Search...' value=""></input>
                <input className="button" id="button" type="submit" value="Search"></input>
              </form>
            </span>
            
            {this.props.children}
          </div>
        );
    }
  }

  ReactDOM.render(
  <Browse />,
  document.getElementById('root')
  );