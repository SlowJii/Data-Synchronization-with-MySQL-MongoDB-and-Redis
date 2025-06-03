CREATE TABLE Actor(
    actor_id BIGINT PRIMARY KEY,
    login VARCHAR(255),
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255)
);

CREATE TABLE Repositories(
    repo_id BIGINT PRIMARY KEY ,
    repo_name VARCHAR(255),
    repo_url VARCHAR(255)
);

CREATE TABLE Payload(
    payload_action VARCHAR(255),

)
