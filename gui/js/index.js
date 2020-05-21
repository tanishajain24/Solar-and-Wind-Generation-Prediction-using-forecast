let {PythonShell} = require('python-shell')
const path = require('path')

const options = {
		scriptPath: path.join(__dirname, '/../engine/')
	}

$('.ui.selection.dropdown')
  .dropdown()
;

$('.ui.dropdown').dropdown("set selected", ["wind"]);


getGeneration = () => {
	const plant = $("#plant").dropdown('get value');
	const city = "London"
	const options = {
		scriptPath: path.join(__dirname, '/../engine/'),
		args: [plant, city]
	}

	predictor = new PythonShell('prediction.py', options)


	gens = []
	$('#data-table').transition('show');
	$("#dimmer").addClass('active')
	predictor.on('message', function(message) {
		// gens = message.split(" ");
		
		gens.push(message)
		if(gens.length === 40){
			let k = 0;
			console.log('hi')
			for(let i = 1; i <= 8; i++){
				console.log('loop 1')
				for(let j = 1; j <= 5; j++){
					document.getElementById('gen-table').rows[i].cells[j].innerHTML = gens[k++]
				}
			}
			$('#dimmer').removeClass('active')
		}
		
	})
		

}


$('#data-table').transition('hide')


$("#predict").on("click", function(){
  getGeneration();
  $('#landing-segment').transition('fly right');
  
});
