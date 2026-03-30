import request from 'supertest';
import { app } from '../../src/index';

describe('Deal summary API integration', () => {
    it('POST /api/deals/summary returns 200 and PDF content-type', async () => {
        const payload = {
            title: 'Strategic Partnership',
            partnerNames: ['Company A', 'Company B'],
            stage: 'Negotiation',
            keyDates: { startDate: '2026-04-01', endDate: '2026-12-31' },
            financialTerms: 'USD 1,000,000'
        };

        const response = await request(app)
            .post('/api/deals/summary')
            .send(payload)
            .expect('Content-Type', /application\/pdf/)
            .expect(200);

        expect(response.headers['content-disposition']).toContain('attachment');
        expect(response.body).toBeInstanceOf(Buffer);
        expect(response.body.length).toBeGreaterThan(10);
    }, 12000);
});