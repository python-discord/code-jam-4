#include "passwordprompt.h"
#include "ui_passwordprompt.h"

PasswordPrompt::PasswordPrompt(QDialog *parent) :
    QDialog(parent),
    ui(new Ui::PasswordPrompt)
{
    ui->setupUi(this);
}

PasswordPrompt::~PasswordPrompt()
{
    delete ui;
}
