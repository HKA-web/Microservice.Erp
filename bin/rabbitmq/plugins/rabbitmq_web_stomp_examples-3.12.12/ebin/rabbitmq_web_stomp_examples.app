{application, 'rabbitmq_web_stomp_examples', [
	{description, "Rabbit WEB-STOMP - examples"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['rabbit_web_stomp_examples_app']},
	{registered, [rabbitmq_web_stomp_examples_sup]},
	{applications, [kernel,stdlib,rabbit_common,rabbit,rabbitmq_web_dispatch,rabbitmq_web_stomp]},
	{optional_applications, []},
	{mod, {rabbit_web_stomp_examples_app, []}},
	{env, [
	    {listener, [{port, 15670}]}
	  ]}
]}.