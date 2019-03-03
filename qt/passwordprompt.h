#ifndef PASSWORDPROMPT_H
#define PASSWORDPROMPT_H

#include <QDialog>

namespace Ui {
class PasswordPrompt;
}

class PasswordPrompt : public QDialog
{
    Q_OBJECT

public:
    explicit PasswordPrompt(QDialog *parent = nullptr);
    ~PasswordPrompt();

private:
    Ui::PasswordPrompt *ui;
};

#endif // PASSWORDPROMPT_H
