// cmdAeolus.cpp : command file
//

#include "StdAfx.h"
#include "AeolusPlugIn.h"

////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
//
// BEGIN Aeolus command
//

#pragma region Aeolus command

// Do NOT put the definition of class CCommandAeolus in a header
// file. There is only ONE instance of a CCommandAeolus class
// and that instance is the static theAeolusCommand that appears
// immediately below the class definition.

class CCommandAeolus : public CRhinoCommand
{
public:
  // The one and only instance of CCommandAeolus is created below.
  // No copy constructor or operator= is required.
  // Values of member variables persist for the duration of the application.

  // CCommandAeolus::CCommandAeolus()
  // is called exactly once when static theAeolusCommand is created.
  CCommandAeolus() = default;

  // CCommandAeolus::~CCommandAeolus()
  // is called exactly once when static theAeolusCommand is destroyed.
  // The destructor should not make any calls to the Rhino SDK. 
  // If your command has persistent settings, then override 
  // CRhinoCommand::SaveProfile and CRhinoCommand::LoadProfile.
  ~CCommandAeolus() = default;

  // Returns a unique UUID for this command.
  // If you try to use an id that is already being used, then
  // your command will not work. Use GUIDGEN.EXE to make unique UUID.
  UUID CommandUUID() override
  {
    // {EFF501A8-9FCE-45D2-A3C8-74AA69E9CFBD}
    static const GUID AeolusCommand_UUID =
    { 0xEFF501A8, 0x9FCE, 0x45D2, { 0xA3, 0xC8, 0x74, 0xAA, 0x69, 0xE9, 0xCF, 0xBD } };
    return AeolusCommand_UUID;
  }

  // Returns the English command name.
  // If you want to provide a localized command name, then override 
  // CRhinoCommand::LocalCommandName.
  const wchar_t* EnglishCommandName() override { return L"Aeolus"; }

  // Rhino calls RunCommand to run the command.
  CRhinoCommand::result RunCommand(const CRhinoCommandContext& context) override;
};

// The one and only CCommandAeolus object
// Do NOT create any other instance of a CCommandAeolus class.
static class CCommandAeolus theAeolusCommand;

CRhinoCommand::result CCommandAeolus::RunCommand(const CRhinoCommandContext& context)
{
  // CCommandAeolus::RunCommand() is called when the user
  // runs the "Aeolus".

  // TODO: Add command code here.

  // Rhino command that display a dialog box interface should also support
  // a command-line, or scriptable interface.

  ON_wString str;
  str.Format(L"The \"%s\" command is under construction.\n", EnglishCommandName());
  const wchar_t* pszStr = static_cast<const wchar_t*>(str);
  if (context.IsInteractive())
    RhinoMessageBox(pszStr, AeolusPlugIn().PlugInName(), MB_OK);
  else
    RhinoApp().Print(pszStr);

  // TODO: Return one of the following values:
  //   CRhinoCommand::success:  The command worked.
  //   CRhinoCommand::failure:  The command failed because of invalid input, inability
  //                            to compute the desired result, or some other reason
  //                            computation reason.
  //   CRhinoCommand::cancel:   The user interactively canceled the command 
  //                            (by pressing ESCAPE, clicking a CANCEL button, etc.)
  //                            in a Get operation, dialog, time consuming computation, etc.

  return CRhinoCommand::success;
}

#pragma endregion

//
// END Aeolus command
//
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
