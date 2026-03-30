import { Application, Router } from 'express';
import { DealController } from '../controllers/dealController';

const dealController = new DealController();
const router = Router();

export const setDealRoutes = (app) => {
    app.use('/api/deals', router);

    router.post('/summary', dealController.createDealSummary.bind(dealController));
};