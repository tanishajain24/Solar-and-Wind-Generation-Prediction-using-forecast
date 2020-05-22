let {PythonShell} = require('python-shell')
const path = require('path')

const options = {
		scriptPath: path.join(__dirname, '/../engine/')
	}

$('.ui.selection.dropdown')
  .dropdown()
;

$('#plant').dropdown("set selected", ["wind"]);
$('#city').dropdown("set selected", ["Berlin"]);


getGeneration = () => {
	const plant = $("#plant").dropdown('get value');
	const city = $("#city").dropdown('get value')
	const options = {
		scriptPath: path.join(__dirname, '/../engine/'),
		args: [plant, city]
	}

	predictor = new PythonShell('prediction.py', options)


	gens = []
	$('#data-table').transition({
	    animation  : 'fly right',
	    duration   : '1s',
	    onComplete : loader
	  });
	
	predictor.on('message', function(message) {
		// gens = message.split(" ");
		gens.push(message)
		console.log(message)
		fillTable(gens)
		
	})
}

loader = () => {
	$("#dimmer").addClass('active')
}

fillTable = (gens) => {
	let k = 0;
	for(let i = 1; i <= 5; i++){
		for(let j = 1; j <= 8; j++){
			if(gens[k] == undefined){
				document.getElementById('gen-table').rows[j].cells[i].innerHTML = "Not Available"
			}
			else {
				document.getElementById('gen-table').rows[j].cells[i].innerHTML = gens[k++]
			}
		}
	}
	$('#dimmer').removeClass('active')
}


$('#data-table').transition('hide')


$("#predict").on("click", function(){
  $('#landing-segment').transition({
    animation  : 'fly right',
    duration   : '2s',
    onComplete : getGeneration
  });
  
});

$('#back').on("click", function(){
	$('#data-table').transition('fly right', 2000, function() {
		$('#landing-segment').removeClass('hidden')
		$('#landing-segment').transition('fly-right');
	})
})