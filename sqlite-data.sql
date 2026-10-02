INSERT INTO users (email, hashed_password, first_name, last_name)
VALUES (
    'user@example.com',
    'scrypt:32768:8:1$d8xcnBzrOemd6g5p$a45d3ef6952d3c3fff9a909fde6efc990b06f5c82193fde90006df0983' ||
    'f20f90166c5f7b9de9bc859356ec22c506ae164ae88d536fcf6e5b3f943f6737a36d3f',
    'User',
    ''
)
ON CONFLICT(email) DO UPDATE SET
    hashed_password = excluded.hashed_password,
    first_name = excluded.first_name,
    last_name = excluded.last_name;
