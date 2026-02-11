{application, 'rabbitmq_top', [
	{description, "RabbitMQ Top"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['rabbit_top_app','rabbit_top_extension','rabbit_top_sup','rabbit_top_util','rabbit_top_wm_ets_tables','rabbit_top_wm_process','rabbit_top_wm_processes','rabbit_top_worker']},
	{registered, [rabbitmq_top_sup]},
	{applications, [kernel,stdlib,rabbit_common,rabbit,amqp_client,rabbitmq_management]},
	{optional_applications, []},
	{mod, {rabbit_top_app, []}},
	{env, []},
		{broker_version_requirements, []}
]}.