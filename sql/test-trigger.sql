INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000001, 'test_user_1', '', 'https://api.github.com/users/test_user_1', 'https://avatars.githubusercontent.com/u/9000001');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000002, 'test_user_2', '', 'https://api.github.com/users/test_user_2', 'https://avatars.githubusercontent.com/u/9000002');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000003, 'test_user_3', 'abc', 'https://api.github.com/users/test_user_3', 'https://avatars.githubusercontent.com/u/9000003');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000004, 'test_user_4', 'def', 'https://api.github.com/users/test_user_4', 'https://avatars.githubusercontent.com/u/9000004');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000005, 'test_user_5', '', 'https://api.github.com/users/test_user_5', 'https://avatars.githubusercontent.com/u/9000005');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000006, 'test_user_6', '', 'https://api.github.com/users/test_user_6', 'https://avatars.githubusercontent.com/u/9000006');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000007, 'test_user_7', 'ghi', 'https://api.github.com/users/test_user_7', 'https://avatars.githubusercontent.com/u/9000007');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000008, 'test_user_8', 'jkl', 'https://api.github.com/users/test_user_8', 'https://avatars.githubusercontent.com/u/9000008');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000009, 'test_user_9', '', 'https://api.github.com/users/test_user_9', 'https://avatars.githubusercontent.com/u/9000009');
INSERT INTO Users (user_id, login, gravatar_id, url, avatar_url) VALUES (9000010, 'test_user_10', '', 'https://api.github.com/users/test_user_10', 'https://avatars.githubusercontent.com/u/9000010');

UPDATE Users SET login = 'updated_user_1', gravatar_id = 'updated_1' WHERE user_id = 9000001;
UPDATE Users SET login = 'updated_user_2' WHERE user_id = 9000002;
UPDATE Users SET url = 'https://example.com/updated_user_3' WHERE user_id = 9000003;
UPDATE Users SET avatar_url = 'https://example.com/avatar/4' WHERE user_id = 9000004;
UPDATE Users SET login = 'another_update_5', url = 'https://example.com/5' WHERE user_id = 9000005;
UPDATE Users SET gravatar_id = 'updated_id_6' WHERE user_id = 9000006;
UPDATE Users SET login = 'user_7_new_login' WHERE user_id = 9000007;
UPDATE Users SET url = 'https://api.new-url.com/users/8' WHERE user_id = 9000008;
UPDATE Users SET avatar_url = 'https://new-avatar.com/u/9' WHERE user_id = 9000009;
UPDATE Users SET login = 'final_user_10', gravatar_id = 'final_id' WHERE user_id = 9000010;

DELETE FROM Users WHERE user_id = 9000001;
DELETE FROM Users WHERE user_id = 9000002;
DELETE FROM Users WHERE user_id = 9000003;
DELETE FROM Users WHERE user_id = 9000004;
DELETE FROM Users WHERE user_id = 9000005;
DELETE FROM Users WHERE user_id = 9000006;
DELETE FROM Users WHERE user_id = 9000007;
DELETE FROM Users WHERE user_id = 9000008;
DELETE FROM Users WHERE user_id = 9000009;
DELETE FROM Users WHERE user_id = 9000010;

