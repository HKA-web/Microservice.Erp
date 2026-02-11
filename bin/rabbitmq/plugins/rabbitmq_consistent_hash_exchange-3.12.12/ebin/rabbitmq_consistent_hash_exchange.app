{application, 'rabbitmq_consistent_hash_exchange', [
	{description, "Consistent Hash Exchange Type"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['Elixir.RabbitMQ.CLI.Diagnostics.Commands.ConsistentHashExchangeRingStateCommand','rabbit_db_ch_exchange','rabbit_exchange_type_consistent_hash']},
	{registered, []},
	{applications, [kernel,stdlib,rabbit_common,rabbit]},
	{optional_applications, []},
	{env, []},
		{broker_version_requirements, []}
]}.