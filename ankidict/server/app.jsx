var Sidebar = React.createClass({
  render: function() {
    return (
      <nav id="sidebar">
          <a href="#"> Nav link 1 </a> <hr />
          <a href="#"> Nav link 2 </a> <hr />
          <a href="#"> Nav link 3 </a> <hr />
          <a href="#"> Nav link 4 </a> <hr />
          <a href="#"> Nav link 5 Bl a h b l a h b l a h b l a h b l a h</a> <hr />
      </nav>
    )
  }
})

var AnswerButton = React.createClass({
  handleClick: function() {
    $.post("http://localhost:9090/api/" + this.props.button_name, function(data){
      location.reload()
    })
  },
  render: function(){
    return (
      <button onClick={this.handleClick} id={this.props.button_name + '_button'}>
        {this.props.button_name}
        <span className="gray"> {this.props.interval} </span>
      </button>
    )
  }
})

var ReviewerModal = React.createClass({
  getInitialState: function() {
    return {buttons: []}
  },
  componentDidMount: function() {
    var this_ = this
    $.getJSON("http://localhost:9090/api/buttons", function(buttons) {
      $.getJSON("http://localhost:9090/api/intervals", function(intervals) {
        $.getJSON("http://localhost:9090/api/card", function(card) {
          $.getJSON("http://localhost:9090/api/remaining", function(remaining) {
            this_.setState({
              buttons: buttons,
              intervals: intervals,
              card: card,
              remaining: remaining,
              show_answer: false,
            })
            $("#answer_textbox").delay(100).focus()
          })
        })
      })
    })
  },
  handleShowAnswer: function(e) {
    e.preventDefault()
    this.setState({
      show_answer: true,
    })
    $("#good_button").focus()
  },
  handleClose: function() {
    $.get("http://localhost:9090/api/deactivate", function(data){})
  },
  render: function() {
    var this_ = this
    return (
      <div id="reviewer_modal">
          <header>
            <button onClick={this.handleClose}>&times;</button>
            <b><span className="gray">Review deck:&nbsp;</span>
              {(this.state.card) ? (this.state.card.deck) : ("Loading...")}
            </b>
            {
              (this.state.remaining) ? (
                <span>
                  <hr />
                  {
                    this.state.remaining['now'] == 'new' ? (
                      <u> New: {this.state.remaining['new']} </u>
                    ) : (
                      <span> New: {this.state.remaining['new']} </span>
                    )
                  }
                  <hr />
                  {
                    this.state.remaining['now'] == 'learning' ? (
                      <u> Learning: {this.state.remaining['learning']} </u>
                    ) : (
                      <span> Learning: {this.state.remaining['learning']} </span>
                    )
                  }
                  <hr />
                  {
                    this.state.remaining['now'] == 'to_review' ? (
                      <u> To review: {this.state.remaining['to_review']} </u>
                    ) : (
                      <span> To review: {this.state.remaining['to_review']} </span>
                    )
                  }
                </span>
              ) : (<span> <span className="vr"></span> Loading... </span>)
            }
          </header>
          {(this.state.card && this.state.buttons && this.state.intervals) ? (
            (this.state.card.finished) ? (
              <main>
                <h2>
                  Congratulations! You have finished this deck for now.
                </h2>
              </main>
            ) : (
              <main>
                <div dangerouslySetInnerHTML={{__html: this.state.card.question}}></div>
                <form action="#" onSubmit={this.handleShowAnswer}>
                  <input type="text" id="answer_textbox" />
                  <button type="submit">
                    Show answer
                  </button>
                </form>
                <div
                  dangerouslySetInnerHTML={{__html: this.state.card.answer}}
                  style={{display: this.state.show_answer ? "initial" : "none"}}
                ></div>
                <hr />
                {this.state.buttons.map(function(name, i){
                  return (<AnswerButton
                    button_name={name}
                    key={name}
                    interval={this_.state.intervals[name]}
                  />);
                })}
              </main>
          )) : (<main> <h2> Loading... </h2> </main>)}
      </div>
    );
  },
})

var MainApp = React.createClass({
  render: function() {
    return(
      <div>
        <input type="checkbox" id="sidebar-hidden-checkbox" />
        <div className="container">
          <label htmlFor="sidebar-hidden-checkbox">☰</label>
          <Sidebar />
        </div>
      </div>
    )
  }
})

$(function(){
  ReactDOM.render(
    React.createElement(MainApp, null),
    document.getElementById('application_root')
  )
})
