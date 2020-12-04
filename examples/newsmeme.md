[newsmeme.comments]
    id {label:"NULLABLE(INTEGER)"}
    author_id {label:"NULLABLE(INTEGER)"}
    post_id {label:"NULLABLE(INTEGER)"}
    parent_id {label:"NULLABLE(INTEGER)"}
    comment {label:"NULLABLE(STRING)"}
    date_created {label:"NULLABLE(DATETIME)"}
    score {label:"NULLABLE(INTEGER)"}
    votes {label:"NULLABLE(STRING)"}
[newsmeme.post_tags]
    post_id {label:"NULLABLE(INTEGER)"}
    tag_id {label:"NULLABLE(INTEGER)"}
[newsmeme.posts]
    id {label:"NULLABLE(INTEGER)"}
    author_id {label:"NULLABLE(INTEGER)"}
    title {label:"NULLABLE(STRING)"}
    description {label:"NULLABLE(STRING)"}
    link {label:"NULLABLE(STRING)"}
    date_created {label:"NULLABLE(DATETIME)"}
    score {label:"NULLABLE(INTEGER)"}
    num_comments {label:"NULLABLE(INTEGER)"}
    votes {label:"NULLABLE(STRING)"}
    access {label:"NULLABLE(INTEGER)"}
    tags {label:"NULLABLE(STRING)"}
[newsmeme.tags]
    id {label:"NULLABLE(INTEGER)"}
    slug {label:"NULLABLE(STRING)"}
    nam {label:"NULLABLE(STRING)"}
[newsmeme.users]
    id {label:"NULLABLE(INTEGER)"}
    username {label:"NULLABLE(STRING)"}
    email {label:"NULLABLE(STRING)"}
    karma {label:"NULLABLE(INTEGER)"}
    date_joined {label:"NULLABLE(DATETIME)"}
    activation_key {label:"NULLABLE(STRING)"}
    role {label:"NULLABLE(INTEGER)"}
    receive_email {label:"NULLABLE(BOOLEAN)"}
    email_alerts {label:"NULLABLE(BOOLEAN)"}
    followers {label:"NULLABLE(STRING)"}
    following {label:"NULLABLE(STRING)"}
    password {label:"NULLABLE(STRING)"}
    openid {label:"NULLABLE(STRING)"}
newsmeme.users ?--* newsmeme.comments
newsmeme.posts ?--* newsmeme.comments
newsmeme.comments ?--* newsmeme.comments
newsmeme.posts ?--* newsmeme.post_tags
newsmeme.tags ?--* newsmeme.post_tags
newsmeme.users ?--* newsmeme.posts