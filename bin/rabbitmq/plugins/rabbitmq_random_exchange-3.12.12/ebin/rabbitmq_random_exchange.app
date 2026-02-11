{application, 'rabbitmq_random_exchange', [
	{description, "RabbitMQ Random Exchange"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['rabbit_exchange_type_random']},
	{registered, []},
	{applications, [kernel,stdlib,rabbit_common,rabbit]},
	{optional_applications, []},
	{env, []}
]}.