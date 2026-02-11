{application, 'rabbitmq_shovel_management', [
	{description, "Management extension for the Shovel plugin"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['rabbit_shovel_mgmt','rabbit_shovel_mgmt_util']},
	{registered, []},
	{applications, [kernel,stdlib,rabbit_common,rabbit,rabbitmq_management,rabbitmq_shovel]},
	{optional_applications, []},
	{env, []},
		{broker_version_requirements, []}
]}.