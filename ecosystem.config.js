module.exports = {
  apps: [
    {
      name: "SolawiKatari",
      script: "mail-form.py",
      interpreter: "python3",
      env: {
        FLASK_ENV: "production",
      },
      cwd: "/var/www/solawi.katari.farm,
    },
  ],
};
