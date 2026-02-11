{application, 'amqp10_client', [
	{description, "AMQP 1.0 client from the RabbitMQ Project"},
	{vsn, "3.12.12"},
	{id, "v3.12.12"},
	{modules, ['amqp10_client','amqp10_client_app','amqp10_client_connection','amqp10_client_connection_sup','amqp10_client_connections_sup','amqp10_client_frame_reader','amqp10_client_session','amqp10_client_sessions_sup','amqp10_client_sup','amqp10_client_types','amqp10_msg']},
	{registered, [amqp10_client_sup]},
	{applications, [kernel,stdlib,ssl,inets,crypto,public_key,amqp10_common,credentials_obfuscation]},
	{optional_applications, []},
	{mod, {amqp10_client_app, []}},
	{env, []},
	%% Hex.pm package informations.
	{licenses, ["MPL-2.0"]},
	{links, [
	    {"Website", "https://www.rabbitmq.com/"},
	    {"GitHub", "https://github.com/rabbitmq/rabbitmq-server/tree/main/deps/amqp10_client"}
	  ]},
	{build_tools, ["make", "rebar3"]},
	{files, [
	    	    "erlang.mk",
	    "git-revisions.txt",
	    "include",
	    "LICENSE*",
	    "Makefile",
	    "rabbitmq-components.mk",
	    "README",
	    "README.md",
	    "src"
	  ]}
]}.