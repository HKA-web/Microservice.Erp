{application, 'rabbitmq_recent_history_exchange', [
	{description, "RabbitMQ Recent History Exchange"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['rabbit_db_rh_exchange','rabbit_exchange_type_recent_history']},
	{registered, []},
	{applications, [kernel,stdlib,rabbit_common,rabbit]},
	{optional_applications, []},
	{env, []},
		{broker_version_requirements, []}
]}.