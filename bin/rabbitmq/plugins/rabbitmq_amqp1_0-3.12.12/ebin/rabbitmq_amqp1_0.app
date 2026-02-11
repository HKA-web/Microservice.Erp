{application, 'rabbitmq_amqp1_0', [
	{description, "AMQP 1.0 support for RabbitMQ"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['Elixir.RabbitMQ.CLI.Ctl.Commands.ListAmqp10ConnectionsCommand','rabbit_amqp1_0','rabbit_amqp1_0_channel','rabbit_amqp1_0_incoming_link','rabbit_amqp1_0_link_util','rabbit_amqp1_0_message','rabbit_amqp1_0_outgoing_link','rabbit_amqp1_0_reader','rabbit_amqp1_0_session','rabbit_amqp1_0_session_process','rabbit_amqp1_0_session_sup','rabbit_amqp1_0_session_sup_sup','rabbit_amqp1_0_util','rabbit_amqp1_0_writer']},
	{registered, []},
	{applications, [kernel,stdlib,rabbit_common,rabbit,amqp_client,amqp10_common]},
	{optional_applications, []},
	{env, [
	    {default_user, "guest"},
	    {default_vhost, <<"/">>},
	    {protocol_strict_mode, false}
	  ]},
		{broker_version_requirements, []}
]}.