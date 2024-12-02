DELETE FROM suspensions;
DELETE FROM direct_messages;
DELETE FROM channel_messages;
DELETE FROM messages;
DELETE FROM community_members;
DELETE FROM users;
DELETE FROM channels;
DELETE FROM communities;

ALTER SEQUENCE channels_id_seq RESTART 1;
ALTER SEQUENCE communities_id_seq RESTART 1;
ALTER SEQUENCE users_id_seq RESTART 1;
ALTER SEQUENCE messages_id_seq RESTART 1;
ALTER SEQUENCE suspensions_id_seq RESTART 1;

INSERT INTO communities(name) VALUES
	('Arrakis'),
	('Comedy');

INSERT INTO channels(community_id, name) VALUES
	(1, 'Worms'), -- Arrakis
	(1, 'Random'), -- Arrakis
	(2, 'ArgumentClinic'), -- Comedy
	(2, 'Dialogs'); -- Comedy

INSERT INTO users(username, email, password, session_key) VALUES
	('Abbott', 'abbott@example.com', 'fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64', NULL),
	('Costello', 'costello@example.com', 'df5225264223c7ef81ec794a3f18f04a10e81626f3209b347a8f624f487ea8c710a08bd5d8dab18ba5e4fa9171898f5c369b9521670c7519b4461dfac0ecd6ec', NULL),
	('Moe', 'moe@example.com', '2d85e278623d5064b613a4a4e73b0a72c3db5b990bc97e6191a75dd072a90e6989e00d112e0ee6308b4037568d0694670566ac2e174a026357594ca20771ace6', NULL),
	('Larry', 'larry@example.com', '4b6763bc455c52e398092edd1675ab294bae58a5c21c9cfb2315f0d1dac7e1518a1e8448756078edc29f371793193ab76687ea26b503f4473d2378d023ca58a8', NULL),
	('Curly', 'curly@example.com', '94061b9451d424f6d87fd1213d0c6430c95236a6fa6c15ed06973ca9f94430f1268e27a7c0aafe60ff66ad737ffc6591e73371b018d8a8e490baac536812f4e6', NULL),
	('spicelover', 'spicelover@hotmail.com', 'abbbb1f4ab1226d216ae27f42acfb2589107830adb24e370f50c6e5a351f691f5e9bf054a8bbe58b6daee3b57ce047f21ca20066b9f0e4c192c07a9ae73bad3b',
	NULL),
	('Paul', NULL, '005a472e445941428bf3defa9b4cb0f7c6ba42ea974f5641a4e98246f20147c9a8bd5228b016b0f57671d1968159c3374af8da8f4a603dcf9b8ed399ccf401cf',
	'ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3');

INSERT INTO community_members(community_id, user_id) VALUES
	(2, 1), -- Abbott in Comedy
	(2, 2), -- Costello in Comedy
	(2, 3), -- Moe in Comedy
	(2, 4), -- Larry in Comedy
	(2, 5), -- Curly in Comedy
	(1, 6); -- spicelover in Arrakis

INSERT INTO suspensions(user_id, community_id, expiration_time) VALUES
	(4, 2, '2060-01-01 00:00:00'), -- Larry suspended from Comedy
	(5, 2, '1990-12-31 00:00:00'), -- Curly suspended from Comedy
	(7, 1, '1990-12-31 00:00:00'); -- Paul suspended from Arrakis

INSERT INTO messages(sender_user_id, message, time_sent, is_read) VALUES
 	(1, 'Hello', '1922-01-01 00:00:00', false), -- 1 Abbott
	(2, 'Hi', '1922-01-01 00:01:00', false), -- 2 Costello
	(2, 'Hi', '1922-01-01 00:01:00', false), -- 3 Costello
	(1, 'Yo', '1932-01-01 00:02:00', true), -- 4 Abbott
	(1, 'Hey', '1970-01-01 00:02:00', false), -- 5 Abbott
	(1, 'How are you', '1970-01-01 00:02:00', true), -- 6 Abbott
	(2, 'Good', '1995-01-01 00:02:00', false), -- 7 Costello
	(4, 'Sup', '1995-03-02 00:02:00', false), -- 8 Larry
	(2, 'Fine', '1970-01-01 00:02:00', true), -- 9 Costello
	(7, 'Hello Moe', '2024-12-09 00:08:00', true), -- 10 Paul
	(3, 'Hi Paul', '2024-12-09 00:08:01', true), -- 11 Moe
	(7, 'How are you?', '2024-12-09 00:08:02', true), -- 12 Paul
	(3, 'I''m fine', '2024-12-09 00:08:01', true), -- 13 Moe
	(5, 'please reply', '2024-12-01 00:02:00', true), -- 14 Curly
	(6, 'i replied already!', '2024-12-01 00:02:05', true), -- 15 spicelover
	(6, 'A new day', '2024-11-02 00:02:05', true), -- 16 spicelover
	(1, 'Sup dialogs', '2024-11-02 00:02:05', true); -- 17 Abbott

INSERT INTO direct_messages (id, receiver_user_id) VALUES
	(1, 2), -- To Costello
	(2, 1), -- To Abbott
	(3, 1), -- To Abbott
	(4, 5), -- To Curly
	(5, 3), -- To Moe
	(6, 4), -- To Larry
	(7, 3), -- To Moe
	(8, 3), -- To Moe
	(9, 4), -- To Larry
	(10, 3), -- To Moe
	(11, 7), -- To Paul
	(12, 3), -- To Moe
	(13, 7); -- To Paul

INSERT INTO channel_messages (id, channel_id) VALUES
	(14, 2), -- To Random
	(15, 2), -- To Random
	(16, 1), -- To Worms
	(17, 4); -- To Dialogs
