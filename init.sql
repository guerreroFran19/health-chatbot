CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS medications (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,  -- Ej: "500mg", "1 tableta"
    frequency_hours INT NOT NULL, -- Cada cuántas horas se toma
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,           -- Opcional: hasta cuándo tomarlo
    instructions TEXT,
    is_active BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_medication_user FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

