# Final deployment checklist

1. Replace `YOUR NGO NAME`, email, phone, office address and social links.
2. Enter only verified mission/history/project/impact information.
3. Upload only real NGO photos/videos with permission/consent and correct credits.
4. Create MySQL database and set `.env`.
5. Run migrations and create an admin.
6. Configure email SMTP.
7. Configure Razorpay/Stripe/PayPal with verified NGO merchant details.
8. Use TEST payment mode first; switch to LIVE only after successful verification.
9. Configure HTTPS and production `DEBUG=False`.
10. Set `ALLOWED_HOSTS`.
11. Run `python manage.py collectstatic`.
12. Deploy on a free backend-capable server and keep the live domain available after each module.
13. Push each completed module to GitHub and maintain the README.
