COMMENT ON COLUMN table_1.persistence_token IS 'anon: [{"mutation_name": "empty_string"}]';
COMMENT ON COLUMN table_1.crypted_password IS 'anon: [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3125d3bd1ett18ffc4a8092e2616b9e5ca7954b2c52504"}}]';
COMMENT ON COLUMN table_1.text IS 'anon: [{"mutation_name": "string_by_mask", "mutation_kwargs": {"mask": "test chars: @@@@@; test digits: #####;"}}]';

COPY table_1 (id, crypted_password, persistence_token, text) FROM stdin;
07750c56-fb37-46e1-b7b6-da530704c056	400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3255d3bd1edd18ffc4a8092e2616b9e5ca7954b2c52504	86a97ff982e87ed5af7d90ab2ce31d4e89a3af3e6a0490b067bb8213aea7a4ee0eeafae1d8fe3c6f990aead095092fcf852004b18e484ef22569aebf64c3747f	Test Text
d489bda7-3212-4026-aef9-879d3242ad0c	400$8$50$5555852e67bf920f$161b41afd99159609151f22fbc4efdccb925244606a87fc635954a71e8f7606f	630aaf10f3edcb396181535476bccfd369e1ee9281cbc218d0861e6117b9839219cb403abed3b59468b2564c229d78b0cb610d0e16fa4a03dc4d93ed3d55deb3	Happy New Year
ab344f75-d78a-47ba-a4f7-121275b3b241	400$8$4a$fb1a833f95079502$8b6ddd327381860e18bce53ee1a3249d5237de4f4344c06ad940ba8cfc6a2259	06fa5d0f3a4d62ff60717ff3315301129a5bcd152f63f073b67d2e6a835b098524b1d097367283c97ca75db9154cf61d6a918248eb68eaf8cd83d1a87cdd92dc	Hello
f7bd4a7f-b63f-41c3-83bd-9683f33bb4b3	400$8$50$8368e20d878ef1b1$b271e3af024b424b7256592439a35d6eb224b4dc769ac9f2fa564b282efb8a47	02cbd8d1e9690c7786375f9f6ec4da6fa3c2ead70d41a7aa1d7fe631477b42635210f0e8fa7579f6f4b5afdb364d9465623a2861ecff75fa3a052c9b2a9fc2dd	Nice Try
abe9fd39-f0b3-4ec6-9006-9783fbdade07	400$8$50$ef1eb813f8d8b99d$2932a9dc75d10f13525e43c29726061d99b4ebdff2e9f9951eb6e2393f36d221	b09909b6e83938dd41ffb5e931eeb3d646b1856dfb74a81acb1697b6d8466468047fe92286e011a4634c71b8d8775c7d5a31e19ce111bd31d0a61a4faf93d6af	Every Day
\.

COMMENT ON COLUMN schema.table_1.email IS 'anon: [{"mutation_name": "email"}]';
COMMENT ON COLUMN schema.table_1.password_salt IS 'anon: [{"mutation_name": "null"}]';
COMMENT ON COLUMN schema.table_1.dt_birthday IS 'anon: [{"mutation_name": "date", "mutation_kwargs": {"start": 2000, "end": 2024}}]';
COMMENT ON COLUMN schema.table_1.crypted_password IS 'anon: [{"mutation_name": "fixed_value", "mutation_kwargs": {"value": "400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3125d3bd1ett18ffc4a8092e2616b9e5ca7954b2c52504"}}]';

COPY schema.table_1 (id, email, crypted_password, dt_birthday) FROM stdin;
07750c56-fb37-46e1-b7b6-da530704c056	cj@example.com	400$8$4c$c11df6facaefc6bc$93a657fb3c6e4cd1fd3255d3bd1edd18ffc4a8092e2616b9e5ca7954b2c52504	1996-10-02
d489bda7-3212-4026-aef9-879d3242ad0c	leo@example.com	400$8$50$5555852e67bf920f$161b41afd99159609151f22fbc4efdccb925244606a87fc635954a71e8f7606f	1996-10-03
ab344f75-d78a-47ba-a4f7-121275b3b241	donna@example.com	400$8$4a$fb1a833f95079502$8b6ddd327381860e18bce53ee1a3249d5237de4f4344c06ad940ba8cfc6a2259	2005-01-02
f7bd4a7f-b63f-41c3-83bd-9683f33bb4b3	charlie@example.com	400$8$50$8368e20d878ef1b1$b271e3af024b424b7256592439a35d6eb224b4dc769ac9f2fa564b282efb8a47	2005-10-02
abe9fd39-f0b3-4ec6-9006-9783fbdade07	fun@example.com	400$8$50$ef1eb813f8d8b99d$2932a9dc75d10f13525e43c29726061d99b4ebdff2e9f9951eb6e2393f36d221	2022-12-31
\.
