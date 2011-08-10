$(document).ready(function() {
	curLevel = 0;
	timeLeftInLevel = 0;
	levelScore = 0;
	totalScore = 0;
	$('#id_answer').attr("disabled", true);

	function submitAnswer() {
		if($('#id_answer').attr("disabled")) return;
		$.ajax({
			type: 'POST',
			url: "submitAnswer",
			success: submitAnswerCallback,
			data: {sessionID: sessionID, answer: $("#id_answer").val()}
		});
		$('#id_answer').val('');
	}

	function submitAnswerCallback(argcsv) {
		args = argcsv.split(",");
		if(args[0]=="LEVEL_OVER") {
			if(levelScore!=args[1]) {
				alert("Scoreboard desync!");
			}
			endLevel();
		} else if(args[0]=="GAME_OVER") {
			if(levelScore!=args[1] || totalScore!=args[2]) {
				alert("Scoreboard desync!");
			}
			endLevel();
			endGame();
		} else if (args[0]=="WRONG") {
			$("#answerFeedbackField").text(args[1]+" is incorrect.");
			addScore(-1);
		} else if (args[0]=="INVALID_ANSWER") {
			$("#answerFeedbackField").text("Invalid answer.");
		} else if (args[0]=="NO_QUESTION") {
		} else if (args[0]=="CORRECT") {
			$("#answerFeedbackField").text("Correct.");
			addScore(1);
		}
	}

	function playerReady() {
		$.ajax({
			type: 'POST',
			url: "playerReady",
			success: pollNextLevel,
			data: {sessionID: sessionID}
		});
	}

	function pollNextLevel() {
		$("#nextLevelButton").attr("disabled", true);
		pollNextLevelInterval = setInterval(
											function() {
												$.ajax({
													type: 'POST',
													url: 'pollNextLevel',
													success: pollNextLevelCallback,
													data: {sessionID: sessionID}
												});
												dbg("polling next level");
											}
											, 50
											);
	}

	/*
	*/
	function pollNextLevelCallback(argcsv) {
	// if 'FAIL' --> do nothing
	// if 'SUCCESS' --> levelfield,
	// start polling for next question, stop polling for next level, update UI for in game mode
		args = argcsv.split(",");
		request_status = args[0];
		if (request_status == 'FAIL')
			return;
		clearInterval(pollNextLevelInterval); // disable the polling for next level if the level starts
		curLevel = args[1];
		timeLeftInLevel = args[2];
		dbg("set time to: "+timeLeftInLevel);
		levelScore = 0;
		console.log(levelScore);

		$("#levelField").text("Level: " + curLevel);
		$("#timerField").text("Timer: " + timeLeftInLevel);
		$('#id_answer').removeAttr("disabled");
		$("#scoreField").text("Score: "+levelScore);
		// start timer countdown for next level
		updateTimerInterval = setInterval(function() {
									timeLeftInLevel -= 1;
									$("#timerField").text("Timer: "+timeLeftInLevel);
									if (timeLeftInLevel <= 0) {
										clearInterval(pollNextQuestionInterval);
										clearInterval(updateTimerInterval);
										$('#id_answer').val('');
										submitAnswer();
									}
								}, 1000);
		pollNextQuestion(); // start polling for questions
	}
	function pollNextQuestion() {
		pollNextQuestionInterval = setInterval(function() {
										$.ajax( {
											type: 'POST',
											url: 'pollNextQuestion',
											success: pollNextQuestionCallback,
											data: {sessionID: sessionID}
										});
										
									}, 50);

		
	}
	function pollNextQuestionCallback(argscsv) {
	// if 'FAIL' (the next question is not ready) --> do nothing
	// if 'SUCCESS' --> update the text for next question; update score
		args = argscsv.split(",");
		request_status = args[0];
		if (request_status == 'FAIL')
			dbg("pollNextQuestionCallback FAIL");
		else {
			curQuestion = args[1];
			dbg("curQuestion= " + curQuestion);
			$('#id_answer').val('')
			$("#questionField").text(""+curQuestion);
		}
	}

	function addScore(d) {
		levelScore += d;
		totalScore += d;
		$("#scoreField").text("Score: "+levelScore);
		$("#totalScoreField").text("Total: "+totalScore);
	}
	function endLevel() {
		$("#questionField").text("Level "+curLevel+" over");
		$('#id_answer').attr("disabled", true);
		$("#nextLevelButton").removeAttr('disabled');
	}
	function endGame() {
		$("#questionField").text("Game over");
		$('#nextLevelButton').attr("disabled", true);
	}
	function dbg(str) {
		txt = $("#debug").text();
		//$("#debug").text(str+"\n"+txt);
	}



	// Bind button listeners
	$("#id_answer").keydown(function(event) {
		if (event.keyCode == 13 || event.keyCode == 32) {
			submitAnswer();
		} 
	});
	$("#nextLevelButton").click(function(event) {
		playerReady();
	});
	
}); // end Docuemnt.Ready
