{application, 'osiris', [
	{description, "Foundation of the log-based streaming subsystem for RabbitMQ"},
	{vsn, "1.7.2"},
	{id, "v3.12.12"},
	{modules, ['osiris','osiris_app','osiris_bench','osiris_bloom','osiris_counters','osiris_ets','osiris_log','osiris_log_shared','osiris_replica','osiris_replica_reader','osiris_replica_reader_sup','osiris_retention','osiris_server_sup','osiris_sup','osiris_tracking','osiris_util','osiris_writer']},
	{registered, [osiris_sup]},
	{applications, [kernel,stdlib,sasl,crypto,gen_batch_server,seshat]},
	{optional_applications, []},
	{mod, {osiris_app, []}},
	{env, [
	{data_dir, "/tmp/osiris"},
	{port_range, {6000, 6500}},
	{max_segment_size_chunks, 256000},
	{replication_transport, tcp},
	{replica_forced_gc_default_interval, 4999}
]}
]}.