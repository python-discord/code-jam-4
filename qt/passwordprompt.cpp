#include "passwordprompt.h"
#include "ui_passwordprompt.h"

PasswordPrompt::PasswordPrompt(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::PasswordPrompt)
{
    ui->setupUi(this);
}

PasswordPrompt::~PasswordPrompt()
{
    delete ui;
}
