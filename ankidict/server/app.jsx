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

var ReviewerModal = React.createClass({
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
              <button id="again_button"> Again </button>
              <button id="hard_button">  Hard  </button>
              <button id="good_button">  Good  </button>
              <button id="easy_button">  Easy  </button>
            </div>
            <p id="remaining_text">Remaining text.</p>
          </div>
      </div>
    );
  }
})

var MainApp = React.createClass({
  render: function() {
    return(
      <div>
        <input type="checkbox" id="sidebar-hidden-checkbox" />
        <div class="container">
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
  $("#again_button").click(function(){
    $.get("http://localhost:9090/api/again", function(data){
      location.reload()
    })
  })
  $("#hard_button").click(function(){
    $.get("http://localhost:9090/api/hard", function(data){
      location.reload()
    })
  })
  $("#good_button").click(function(){
    $.get("http://localhost:9090/api/good", function(data){
      location.reload()
    })
  })
  $("#easy_button").click(function(){
    $.get("http://localhost:9090/api/easy", function(data){
      location.reload()
    })
  })
  $("#answer_form").submit(function(e){
    e.preventDefault()
    $("#answer_text").toggle('fast')
    $("#good_button").focus()
  })
  $("#answer_textbox").delay(100).focus()
})
