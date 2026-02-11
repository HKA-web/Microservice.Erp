{application, 'rabbitmq_stream_common', [
	{description, "RabbitMQ Stream Common"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['rabbit_stream_core']},
	{registered, []},
	{applications, [kernel,stdlib]},
	{optional_applications, []},
	{env, [
]}
]}.