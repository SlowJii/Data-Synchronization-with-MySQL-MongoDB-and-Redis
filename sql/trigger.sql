CREATE TABLE IF NOT EXISTS user_log_before(
    user_id BIGINT,
    login VARCHAR(255),
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255),
    action_type VARCHAR(10),
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_log_after(
    user_id BIGINT,
    login VARCHAR(255),
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255),
    action_type VARCHAR(10),
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==================================== TRIGGERS ==================================
DELIMITER //

-- UPDATE TRIGGERS

CREATE TRIGGER before_update_users
BEFORE UPDATE ON Users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_before(user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp)
    VALUES (OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url, 'UPDATE', NOW());
END;
//


CREATE TRIGGER after_update_users
AFTER UPDATE ON Users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_after(user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp)
    VALUES (NEW.user_id, NEW.login, NEW.gravatar_id, NEW.url, NEW.avatar_url, 'UPDATE', NOW());
END;
//

-- INSERT TRIGGER

CREATE TRIGGER after_insert_users
AFTER INSERT ON Users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_after(user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp)
    VALUES (NEW.user_id, NEW.login, NEW.gravatar_id, NEW.url, NEW.avatar_url, 'INSERT', NOW());
END;
//

-- DELETE TRIGGER

CREATE TRIGGER before_delete_users
BEFORE DELETE ON Users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_before(user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp)
    VALUES (OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url, 'DELETE', NOW());
END;
//

DELIMITER ;
