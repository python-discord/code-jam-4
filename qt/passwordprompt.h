#ifndef PASSWORDPROMPT_H
#define PASSWORDPROMPT_H

#include <QWidget>

namespace Ui {
class PasswordPrompt;
}

class PasswordPrompt : public QWidget
{
    Q_OBJECT

public:
    explicit PasswordPrompt(QWidget *parent = nullptr);
    ~PasswordPrompt();

private:
    Ui::PasswordPrompt *ui;
};

#endif // PASSWORDPROMPT_H
