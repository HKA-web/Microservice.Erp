{application, 'rabbitmq_web_mqtt_examples', [
	{description, "Rabbit WEB-MQTT - examples"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['rabbit_web_mqtt_examples_app']},
	{registered, [rabbitmq_web_mqtt_examples_sup]},
	{applications, [kernel,stdlib,rabbit_common,rabbit,rabbitmq_web_dispatch,rabbitmq_web_mqtt]},
	{optional_applications, []},
	{mod, {rabbit_web_mqtt_examples_app, []}},
	{env, [
	    {listener, [{port, 15670}]}
	  ]}
]}.