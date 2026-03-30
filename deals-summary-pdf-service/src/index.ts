import express from 'express';
import bodyParser from 'body-parser';
import { setDealRoutes } from './routes/dealRoutes';

export const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
setDealRoutes(app);

// Start the server only when run directly (not when imported by tests)
if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server is running on http://localhost:${PORT}`);
    });
}