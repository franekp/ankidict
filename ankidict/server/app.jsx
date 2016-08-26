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
      </button>
    )
  }
})

var ReviewerModal = React.createClass({
  getInitialState: function() {
    return {buttons: []}
  },
  componentDidMount: function() {
    this_ = this
    $.getJSON("http://localhost:9090/api/buttons", function(buttons) {
      $.getJSON("http://localhost:9090/api/intervals", function(intervals) {
        this_.setState({
          buttons: buttons,
          intervals: intervals,
        })
      })
    })
  },
  render: function() {
    return (
      <div id="reviewer_modal">
          <div id="reviewer_modal_header">
            <button id="close_button">&times;</button>
            <h2><b>Time for vocabulary!</b></h2>
          </div>
          <div id="reviewer_modal_body">
            <p id="question_text">Question text.</p>
            <form action="#" id="answer_form">
              <input type="text" id="answer_textbox" />
              <button type="submit">
                Show answer
              </button>
            </form>
            <p id="answer_text">Answer text.</p>
            <hr />
            <div id="difficulty_buttongroup">
              {this.state.buttons.map(function(name, i){
                return <AnswerButton button_name={name} key={name} />;
              })}
            </div>
            <p id="remaining_text">Remaining text.</p>
          </div>
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
  $("#question_text").load("http://localhost:9090/api/get_question")
  $("#answer_text").load("http://localhost:9090/api/get_answer")
  $("#remaining_text").load("http://localhost:9090/api/get_remaining")

  $("#close_button").click(function(){
    $.get("http://localhost:9090/api/deactivate", function(data){})
  })
  $("#answer_form").submit(function(e){
    e.preventDefault()
    $("#answer_text").toggle('fast')
    $("#good_button").focus()
  })
  $("#answer_textbox").delay(100).focus()
})
