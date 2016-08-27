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
        <span> {this.props.interval} </span>
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
    this.setState({
      show_answer: true,
    })
    $("#good_button").focus()
  },
  render: function() {
    var this_ = this
    var submit_handler = function(e) {
      e.preventDefault()
      this_.handleShowAnswer()
    }
    return (
      <div id="reviewer_modal">
          <div id="reviewer_modal_header">
            <button id="close_button">&times;</button>
            <h3><span>Review deck:&nbsp;</span>
              {(this.state.card) ? (this.state.card.deck) : ("Loading...")}
            </h3>
            {
              (this.state.remaining) ? (
                <span>
                <span className="vr"></span>
                New: {this.state.remaining['new']}
                <span className="vr"></span>
                Learning: {this.state.remaining['learning']}
                <span className="vr"></span>
                To review: {this.state.remaining['to_review']}
                </span>
              ) : (<span> <span className="vr"></span> Loading... </span>)
            }
          </div>
          {(this.state.card && this.state.buttons && this.state.intervals) ? (
            <div id="reviewer_modal_body">
              <div dangerouslySetInnerHTML={{__html: this.state.card.question}}></div>
              <form action="#" onSubmit={submit_handler}>
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
              <div id="difficulty_buttongroup">
                {this.state.buttons.map(function(name, i){
                  return (<AnswerButton
                    button_name={name}
                    key={name}
                    interval={this_.state.intervals[name]}
                  />);
                })}
              </div>
            </div>
          ) : (<div id="reviewer_modal_body"> <h2> Loading... </h2> </div>)}
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
          <ReviewerModal />
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
  $("#close_button").click(function(){
    $.get("http://localhost:9090/api/deactivate", function(data){})
  })
  
})
