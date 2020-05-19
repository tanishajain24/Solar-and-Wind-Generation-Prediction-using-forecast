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


	$('#data-table').transition('horizontal flip');
	predictor.on('message', function(message) {
		console.log(message)
		
	})

}


$('#data-table').transition('hide')


$("#predict").on("click", function(){
  getGeneration();
  $('#landing-segment').transition('fly right');
});
