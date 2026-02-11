{application, 'rabbitmq_event_exchange', [
	{description, "Event Exchange Type"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['rabbit_event_exchange_decorator','rabbit_exchange_type_event']},
	{registered, []},
	{applications, [kernel,stdlib,rabbit_common,rabbit]},
	{optional_applications, []},
	{env, []},
		{broker_version_requirements, []}
]}.